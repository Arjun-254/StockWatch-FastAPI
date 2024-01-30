from fastapi import Depends, FastAPI, HTTPException, status, Header, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pymongo.errors import DuplicateKeyError


from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
import yfinance as yf

from schemas import User, Login, Token, UserInDB, TokenData, TickerRequest

SECRET_KEY = "c67d75893e1466b33475deac05f91f606bcd1b2fbfa569acb4afdbbc1f4599dc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="YFinance API",)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = MongoClient(
    "mongodb+srv://Aj_3001:RacWMGQ6k9gLKP0g@cluster0.vflcwlu.mongodb.net")
db = conn.yfin.yfin


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user_data = db.find_one({"username": username})
    if user_data:
        return UserInDB(**user_data)
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_user(user: User):
    try:
        db.insert_one({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "hashed_password": get_password_hash(user.password),
            "age": user.age,
            "gender": user.gender,
            "stocks_list": user.stocks_list,
            "watch_list": user.watch_list,
            "first_login": user.first_login,
            "risk": user.risk
        })
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=180)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")
def read_root():
    print(db)
    return {"Hello": "World"}


@app.post('/signup')
def signup(request: User):
    existing_user = db.find_one({"username": request.username})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )

    hashed_pass = get_password_hash(request.password)
    user_object = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "username": request.username,
        "hashed_password": hashed_pass,
        "age": request.age,
        "gender": request.gender,
        "stocks_list": request.stocks_list,
        "watch_list": request.watch_list,
        "first_login": request.first_login,
        "risk": request.risk
    }
    db.insert_one(user_object)
    return {"res": "User succesfully created"}


@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = db.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user found with this {request.username} username')
    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Wrong Username or password')
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer", "first_login": user["first_login"]}


@app.post('/updatelists')
async def updateLists(
    stock_list: list[str] = Body(...),
    watch_list: list[str] = Body(...),
    risk: str = Body(None),
    token: str = Header(...),
):
    current_user = await get_current_user(token)
    filter = {"username": current_user.username}
    newvalues = {
        "$set": {
            "stocks_list": stock_list,
            "watch_list": watch_list,
            "first_login": False,
            "risk": risk,
        }
    }
    db.update_one(filter, newvalues)

    return {"message": "Lists updated successfully"}


@app.post('/getlists')
async def getLists(
    token: str = Header(...),
):
    current_user = await get_current_user(token)
    return {"StockList": current_user.stocks_list, "WatchList": current_user.watch_list, 'Risk': current_user.risk}


@app.post("/yfin")
def stock_data(request: TickerRequest):
    ticker = request.ticker
    stock = yf.Ticker(ticker)
    stock_prices = stock.history(period='1mo')['Close']

    # Convert the DataFrame to an array of objects with 'date' and 'closePrice' properties
    formatted_prices = [
        {"date": str(date), "closePrice": stock_prices[date]} for date in stock_prices.index
    ]

    return formatted_prices

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import image from "./assets/image1.png";

const Navbar = () => {
  const navigate = useNavigate();
  const [logged, setLogged] = useState(false);

  useEffect(() => {
    // Check if JWT token is present in local storage
    const token = localStorage.getItem("jwt");
    if (token) {
      setLogged(true);
    } else {
      setLogged(false);
    }
  }, []); // Empty dependency array ensures that this effect runs only once, similar to componentDidMount

  const handleLogOut = () => {
    // Remove JWT token from local storage on logout
    localStorage.removeItem("jwt");
    setLogged(false);
    navigate("/");
  };

  return (
    <div className="flex flex-row static">
      <header className="absolute inset-x-0 top-0 z-50 bg-gradient-to-r from-blue-600 to-blue-800">
        <nav
          className="flex items-center justify-between p-2 mb-1 lg:px-8"
          aria-label="Global"
        >
          <div className="flex lg:flex-1">
            <a className="p-2 bg-gradient-to-r from-gray-950 via-gray-900 to-gray-950 rounded-lg">
              <p className="text-md md:text-xl font-bold flex justify-center items-left tracking-tight bg-gradient-to-r from-blue-400 to-purple-700 bg-clip-text text-transparent ">
                StockWatch
              </p>
            </a>
          </div>
          <div className="hidden lg:flex lg:gap-x-12">
            <a
              className="text-md font-semibold leading-6 text-gray-200 hover:font-extrabold hover:shadow-xl transition-all ease-in duration-100 p-2 rounded-lg"
              onClick={() => navigate("/")}
            >
              Home
            </a>
          </div>
          <div className="flex flex-1 justify-end">
            {logged ? (
              <>
                <a
                  className="text-sm font-semibold leading-6 text-gray-200 mr-2 p-2 hover:bg-violet-500 rounded-md transition-all duration-500 ease-in-out border-2 border-violet-500"
                  onClick={() => navigate("/preferences")}
                >
                  PREFERENCES
                </a>
                <a
                  className="text-sm font-semibold leading-6 text-gray-200 p-2 hover:bg-violet-500 rounded-md transition-all duration-500 ease-in-out border-2 border-violet-500"
                  onClick={handleLogOut}
                >
                  Log Out <span aria-hidden="true">&rarr;</span>
                </a>
              </>
            ) : (
              <>
                <a
                  className="text-sm font-semibold leading-6 text-gray-200 mr-2 p-2 hover:bg-violet-500 rounded-md transition-all duration-500 ease-in-out border-2 border-violet-500"
                  onClick={() => navigate("/Signup")}
                >
                  Sign Up
                </a>
                <a
                  className="text-sm font-semibold leading-6 text-gray-200 p-2 hover:bg-violet-500 rounded-md transition-all duration-500 ease-in-out border-2 border-violet-500"
                  onClick={() => navigate("/Login")}
                >
                  Log in <span aria-hidden="true">&rarr;</span>
                </a>
              </>
            )}
          </div>
        </nav>
      </header>
    </div>
  );
};

export default Navbar;

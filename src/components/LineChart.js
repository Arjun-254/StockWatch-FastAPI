import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import axios from "axios";
import { InfinitySpin } from "react-loader-spinner";

export default function LineChart({ symbol }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "Price",
        data: [],
        fill: true,
        borderColor: "white",
        tension: 0.4,
      },
    ],
  });

  const [lastClosePrice, setLastClosePrice] = useState("");
  const [secondLastClosePrice, setSecondLastClosePrice] = useState("");
  const [percentageChange, setPercentageChange] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const ticker = symbol === 2 ? "^BSESN" : "^NSEI";
        const response = await axios.post(
          "https://stockwatch-backend-p3zq.onrender.com/yfin",
          {
            ticker: ticker,
          },
          {
            headers: {
              "Content-Type": `application/json`,
            },
          }
        );

        const data = response.data;
        //console.log(data);

        const sortedData = data.sort(
          (a, b) => new Date(a.date) - new Date(b.date)
        );

        if (sortedData.length > 0) {
          const lastClose = sortedData[sortedData.length - 1].closePrice;
          const secondLastClose = sortedData[sortedData.length - 2].closePrice;
          setLastClosePrice(lastClose.toFixed(2).toLocaleString());
          setSecondLastClosePrice(secondLastClose.toFixed(2).toLocaleString());

          // Calculate the percentage change
          const change = lastClose - secondLastClose;
          const percentageChange = ((change / secondLastClose) * 100).toFixed(
            2
          );

          setPercentageChange(percentageChange);
          const lineColor = percentageChange >= 0 ? "green" : "red";

          const chartDataUpdated = {
            labels: sortedData.map((item) => {
              const date = new Date(item.date);
              // Format date and time
              const formattedDateTime = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
              return formattedDateTime;
            }),
            datasets: [
              {
                ...chartData.datasets[0],
                data: sortedData.map((item) => item.closePrice),
                borderColor: lineColor,
                pointRadius: 2,
              },
            ],
          };

          setChartData(chartDataUpdated);
        }
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, [symbol]);

  const chartOptions = {
    scales: {
      x: {
        display: false, // Show x-axis scale and labels
      },
      y: {
        display: true, // Show y-axis scale and labels
      },
    },
    plugins: {
      legend: {
        display: false, // Hide legend
      },
    },
  };

  const colour = percentageChange >= 0 ? "bg-green-600" : "bg-red-600";
  return (
    <>
      {loading ? (
        <div className="bg-gray-800 px-3 py-2 mx-2 rounded-lg flex flex-col w-full">
          <div className="flex flex-row justify-between items-center pb-1">
            {symbol === 1 && (
              <h1 className="text-lg md:text-3xl font-extrabold tracking-tight text-white sm:text-2xl">
                Nifty-50(^NSEI)
              </h1>
            )}
            {symbol === 2 && (
              <h1 className="text-lg md:text-3xl font-extrabold tracking-tight text-white sm:text-2xl">
                Sensex (^BSESN)
              </h1>
            )}
            <InfinitySpin width="200" color="blue" />
          </div>
        </div>
      ) : (
        <div className="bg-gray-800 px-3 py-2 mx-2 rounded-lg flex flex-col w-full">
          <div className="flex flex-row justify-between items-center pb-1">
            {symbol === 1 && (
              <h1 className="text-lg md:text-3xl font-extrabold tracking-tight text-white sm:text-2xl">
                Nifty-50(^NSEI)
              </h1>
            )}
            {symbol === 2 && (
              <h1 className="text-lg md:text-3xl font-extrabold tracking-tight text-white sm:text-2xl">
                Sensex (^BSESN)
              </h1>
            )}
            <p
              className={`ml-2 text-lg md:text-3xl font-extrabold tracking-tight text-white sm:text-xl ${colour} bg-opacity-80 p-1 rounded-lg`}
            >
              {lastClosePrice}
            </p>
          </div>
          <Line data={chartData} options={chartOptions} />
        </div>
      )}
    </>
  );
}

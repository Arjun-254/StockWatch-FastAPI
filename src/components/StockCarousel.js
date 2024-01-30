import React from "react";
import Tilt from "react-parallax-tilt";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Autoplay } from "swiper/modules";
import SwiperCore from "swiper";
import "swiper/css";
import "swiper/css/navigation";

SwiperCore.use([Autoplay, Navigation]);

const stockData = [
  { name: "LT", percentage: 3.91 },
  { name: "ONGC", percentage: 2.0 },
  { name: "NTPC", percentage: 0.93 },
  { name: "SBIN", percentage: 0.87 },
  { name: "TATA M", percentage: 0.74 },
  { name: "KOTAK", percentage: 0.67 },
];

export default function StockCarousel({ color }) {
  const getPercentageColorClass = () => {
    if (color === "green") {
      return "bg-green-600";
    } else if (color === "red") {
      return "bg-red-600";
    }
  };

  return (
    <div className="flex flex-col sm:flex-col md:flex-row justify-cnter w-full overflow-x-auto overflow-y-hidden bg-gray-800 p-2 px-1 rounded-lg">
      <Swiper
        spaceBetween={20}
        slidesPerView={2}
        autoplay={{
          delay: 5000,
          disableOnInteraction: false,
        }}
        modules={[Autoplay, Navigation]}
        style={{ width: "100%" }}
        breakpoints={{
          640: {
            slidesPerView: 3,
          },
        }}
      >
        {stockData.map((stock, index) => (
          <SwiperSlide key={index}>
            <Tilt>
              <li className="flex flex-col justify-center items-center gap-x-6 py-2 px-6 rounded-md bg-gray-700 mx-1">
                <div className="flex gap-x-4">
                  <div className="min-w-0 flex flex-col items-start">
                    <p className="text-sm font-bold leading-5 text-white">
                      {stock.name}
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end">
                  <p
                    className={`mt-1 text-sm leading-5 text-white py-2 px-6 rounded-lg ${getPercentageColorClass()}`}
                  >
                    {`${stock.percentage.toFixed(2)}%`}
                  </p>
                </div>
              </li>
            </Tilt>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
}

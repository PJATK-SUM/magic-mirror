WeatherService = {
  OWAPI_URL: "http://api.openweathermap.org/data/2.5/weather",
  ICON_MAPPING: {
    "01d": "wi-day-sunny",
    "02d": "wi-day-sunny-overcast",
    "03d": "wi-day-cloudy",
    "04d": "wi-cloudy",
    "09d": "wi-day-showers",
    "10d": "wi-day-rain",
    "11d": "wi-day-thunderstorm",
    "13d": "wi-day-snow",
    "50d": "wi-day-fog",
    "01n": "wi-night-clear",
    "02n": "wi-night-partly-cloudy",
    "03n": "wi-night-cloudy",
    "04n": "wi-cloudy",
    "09n": "wi-night-showers",
    "10n": "wi-night-rain",
    "11n": "wi-night-thunderstorm",
    "13n": "wi-night-snow",
    "50n": "wi-night-fog"
  },
  DESCRIPTION_MAPPING: {
    "clear sky": "bezchmurnie",
    "few clouds": "mało chmur",
    "scattered clouds": "małe zachmurzenie",
    "broken clouds": "pochmurnie",
    "shower rain": "przelotne deszcze",
    "rain": "deszcz",
    "thunderstorm": "burza",
    "snow": "śnieg",
    "mist": "mgła"
  },
  fetchWeather: function (callback) {
    let params = {
      query: "units=metric&q=Warsaw,pl&APPID=" + process.env.OWAPI_KEY
    };

    HTTP.get(WeatherService.OWAPI_URL, params, function (error, result) {
      let readings = result.data.weather;
      let main = result.data.main;

      if (readings.length > 0) {
        let reading = readings[0];
        let icon = reading.icon;
        let description = reading.description;

        Weather.insert({
          icon: WeatherService.ICON_MAPPING[icon],
          temperature: main.temp,
          pressure: main.pressure,
          humidity: main.humidity,
          description: WeatherService.DESCRIPTION_MAPPING[description],
          createdAt: new Date()
        });
      }
    });
  }
};

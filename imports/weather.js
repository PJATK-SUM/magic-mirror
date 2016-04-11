import { Mongo } from "meteor/mongo";

class WeatherCollection extends Mongo.Collection {

};

export const Weather = new WeatherCollection("Weather")

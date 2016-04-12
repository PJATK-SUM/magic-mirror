import { Mongo } from "meteor/mongo";

class NewsCollection extends Mongo.Collection {

};

export const News = new NewsCollection("News");

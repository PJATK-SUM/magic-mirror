import moment from "moment";
import { HTTP } from "meteor/http";
import { News } from "./news.js";

export const NewsService = {
  RSS_URL: "https://pja-rss.herokuapp.com/?format=json",
  fetchNews: function(callback) {
    let params = {
      format: "json"
    };

    HTTP.get(NewsService.RSS_URL, function (error, result) {
      if (error) {
        console.log("Error fetching news");
      } else {
        if (result.data && result.data.length > 0) {
          for (let item of result.data) {
            var date = moment(item.published_at, "YYYY-MM-DD").toDate();
            News.upsert({ newsId: item.id }, {
              newsId: item.id,
              title: item.title,
              url: item.url,
              content: item.content,
              publishedAt: date,
              createdAt: new Date()
            });
          }
        }
      }
    });
  }
};

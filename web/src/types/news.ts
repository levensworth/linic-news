import data from '../result.json';
export interface ArticleSource {
  id: string;
  title: string;
  sourceName: string;
  sourceIcon: string;
  url: string;
}

export interface NewsItem {
  id: string;
  title: string;
  date: string;
  labels: string[];
  coverImage: string;
  description: string;
  summary: string;
  sources: ArticleSource[];
  content: string;
}



console.log(data);
export const mockNews: NewsItem[] = data as NewsItem[];


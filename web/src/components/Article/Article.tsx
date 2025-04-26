import { mockNews, NewsItem } from "src/types/news";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { Link, useParams } from "react-router-dom";
import { Button } from "../ui/button";
import ReactMarkdown from "react-markdown";
import NavBar from "../NavBar";

export default function Article() {
    
    const { slug } = useParams();
    

    const news = mockNews.filter(article => article.id == slug)[0];
    

  return (
    <div className="min-h-screen flex flex-col">
    <NavBar />
    
    <div className="container mx-auto px-4 py-8">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-3xl">{news.title}</CardTitle>
          <p className="text-sm text-gray-500">{news.date}</p>
        </CardHeader>
        <CardContent>
          <img
            src={`data:image/jpeg;base64,${news.coverImage}`}
            alt={news.title}
            width={800}
            height={400}
            className="w-full max-h-[1000px] object-cover mb-4 rounded-lg"
          />
          <h2 className="text-xl font-semibold mb-2">Summary</h2>
            <div className="prose lg:prose-xl min-w-full">
            <ReactMarkdown>{news.summary}</ReactMarkdown>
            </div>
          <h2 className="text-xl font-semibold mb-2">Labels</h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {news.labels.map((label) => (
              <Badge key={label} variant="secondary">
                {label}
              </Badge>
            ))}
          </div>
          <h2 className="text-xl font-semibold mb-2">Sources</h2>
          <div className="flex flex-wrap gap-2">
            {news.sources.map((source) => (
              <Link to={source.url} target="_blank">
              <Button
                key={source.id}
                variant="outline"
                className="flex items-center gap-2"
              >
                <img
                  src={source.sourceIcon}
                  alt={source.sourceName}
                  width={16}
                  height={16}
                  className="rounded-full"
                />
                {source.sourceName}
              </Button>
              </Link>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Full Article Section */}
      <Card className="mb-8">
        <CardContent className="pt-6">
          <div className="prose lg:prose-xl text-center min-w-full">
          <ReactMarkdown>{news.content}</ReactMarkdown>
          </div>
        </CardContent>
      </Card>

      {/* Source Articles Section */}
      <Card>
        <CardContent className="pt-6">
          <h2 className="text-xl font-semibold mb-4">Sources</h2>
          <div className="flex flex-wrap gap-2 mb-6">
            {news.sources.map((article) => (
              <Link to={article.url} target="_blank">
              <Button
                key={article.id}
                variant="outline"
                className="flex items-center gap-2"
              >
                <img
                  src={article.sourceIcon || "/placeholder.svg"}
                  alt={article.sourceName}
                  width={16}
                  height={16}
                  className="rounded-full"
                />
                {article.sourceName}
              </Button>
              </Link>
            ))}
          </div>
        </CardContent>
      </Card>
      
    </div>
    </div>
  )
}


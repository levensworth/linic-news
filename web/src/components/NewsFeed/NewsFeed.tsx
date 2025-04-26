

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Link } from "react-router-dom"
import { Badge } from "../ui/badge"
import { mockNews, NewsItem } from "src/types/news"
import NavBar from "../NavBar"

export default function NewsFeed() {
  return (
    <div className="container mx-auto px-4 py-8">
      <NavBar/>
      <h1 className="text-3xl font-bold text-center mb-6 py-3">What's New?</h1>
      <div className="space-y-6">
        {mockNews.map((item: NewsItem) => (
          <Link to={`/news/${item.id}`} key={item.id}>
            <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300 border-y-2 max-h-56">
              <div className="md:flex">
                <div className="md:w-1/3">
                
                  <img
                    src={`data:image/jpeg;base64,${item.coverImage}`}
                    alt={item.title}
                    className="object-contain"
                  />
                </div>
                <div className="md:w-2/3">
                  <CardHeader>
                    <CardTitle>{item.title}</CardTitle>
                    <p className="text-sm text-gray-500">{item.date}</p>
                  </CardHeader>
                  <CardContent>
                    <p className="mb-4">{item.description}</p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {item.labels.map((label) => (
                        <Badge key={label} variant="secondary">
                          {label}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-sm text-gray-600">
                      <strong>Sources:</strong> {item.sources.map(source => source.sourceName).join(', ')}
                    </div>
                  </CardContent>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}

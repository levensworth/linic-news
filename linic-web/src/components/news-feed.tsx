import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"
import Link from "next/link"
import { mockNews, NewsItem } from "@/types/news"
import { NavBar } from "./nav-bar"

export default function NewsFeed() {
  return (
    <div className="min-h-screen flex flex-col">
        <NavBar />
        
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Lo Ultimo</h1>
      <div className="space-y-6">
        {mockNews.map((item: NewsItem) => (
          <Link href={`/news/${item.id}`} key={item.id}>
            <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300">
              <div className="md:flex">
                <div className="md:w-1/3">
                  <Image
                    src={item.coverImage}
                    alt={item.title}
                    width={400}
                    height={200}
                    className="w-full h-48 object-cover"
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
                      <strong>Sources:</strong> {item.sources.join(', ')}
                    </div>
                  </CardContent>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
    </div>
  )
}


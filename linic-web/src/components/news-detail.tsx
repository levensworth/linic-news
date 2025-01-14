'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import Image from "next/image"
import { Article, NewsItem } from '@/types/news'
import { NavBar } from './nav-bar'


export default function NewsDetail({ news }: { news: NewsItem }) {
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null)

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
          <Image
            src={news.coverImage}
            alt={news.title}
            width={800}
            height={400}
            className="w-full h-64 object-cover mb-4 rounded-lg"
          />
          <h2 className="text-xl font-semibold mb-2">Summary</h2>
          <p className="mb-4">{news.summary}</p>
          <h2 className="text-xl font-semibold mb-2">Labels</h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {news.labels.map((label) => (
              <Badge key={label} variant="secondary">
                {label}
              </Badge>
            ))}
          </div>
          <h2 className="text-xl font-semibold mb-2">Articles</h2>
          <div className="flex flex-wrap gap-2">
            {news.articles.map((article) => (
              <Button
                key={article.id}
                variant="outline"
                className="flex items-center gap-2"
                onClick={() => setSelectedArticle(article)}
              >
                <Image
                  src={article.sourceIcon}
                  alt={article.source}
                  width={16}
                  height={16}
                  className="rounded-full"
                />
                {article.source}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>
      {selectedArticle && (
        <Card>
          <CardHeader className="sticky top-0 bg-white z-10 flex flex-row items-center">
            <Image
              src={selectedArticle.sourceIcon}
              alt={selectedArticle.source}
              width={32}
              height={32}
              className="rounded-full mr-2"
            />
            <CardTitle>{selectedArticle.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[calc(100vh-200px)] pr-4">
              <article className="prose max-w-none">
                {selectedArticle.content.split('\n\n').map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </article>
            </ScrollArea>
          </CardContent>
        </Card>
      )}
    </div>
    </div>
  )
}


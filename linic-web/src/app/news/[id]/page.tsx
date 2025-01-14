
import NewsDetail from '@/components/news-detail'
import { mockNews } from '@/types/news'
import { notFound } from 'next/navigation'

export default async function NewsDetailPage({ params }: { params: { id: string } }) {
  const {id} = await params;

  const news = mockNews.find(item => item.id === id)

  if (!news) {
    notFound()
  }

  return <NewsDetail news={news} />
}


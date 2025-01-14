'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from "@/components/ui/button"

const categories = ['All', 'Technology', 'Environment', 'Politics', 'Space', 'Business']

export function NavBar() {
  const pathname = usePathname()
  const [activeCategory, setActiveCategory] = useState('All')

  const handleCategoryChange = (category: string) => {
    setActiveCategory(category)
  }

  return (
    <nav className="sticky top-0 z-50 bg-background border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold">
            News Aggregator
          </Link>
          <div className="flex space-x-2 overflow-x-auto pb-2 md:pb-0">
            {categories.map((category) => (
              <Button
                key={category}
                variant={activeCategory === category ? "default" : "ghost"}
                onClick={() => handleCategoryChange(category)}
                className="whitespace-nowrap"
              >
                {category}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}


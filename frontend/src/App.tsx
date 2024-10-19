'use client'

import { useState, useRef, useEffect } from 'react'
// import Turnstile, { useTurnstile } from "react-turnstile";

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle, Github, ExternalLink } from "lucide-react"

import "./App.css"


const fantasicLoadingText = [
  'Finding Elon Musk...',
  'Generating BlueSky...',
  'Creating Circle...',
  'Uninstalling X...',
  'Banning by Elon Musk...',
  'Launching Rocket...',
]

export default function Component() {
  // const turnstile = useTurnstile()
  const [handle, setHandle] = useState('')
  const [captchaKey,] = useState('')
  const [imageData, setImageData] = useState<string | null>(null)
  const [backgroundColor, setBackgroundColor] = useState('#0085ff')
  const [isLoading, setIsLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('Generating...')
  const [error, setError] = useState<string | null>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    setImageData(null)
    // turnstile.reset()
    try {
      const response = await fetch(`/generate`, {
        method: 'POST',
        body: new URLSearchParams({ handle, captchaKey }),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const blob = await response.blob()
      const reader = new FileReader()
      reader.onloadend = () => {
        const base64data = reader.result as string
        setImageData(base64data)
      }
      reader.readAsDataURL(blob)
    } catch (error) {
      console.error('Error fetching image:', error)
      setError('Failed to generate image. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setLoadingText(fantasicLoadingText[Math.floor(Math.random() * fantasicLoadingText.length)])
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [isLoading])

  useEffect(() => {
    if (imageData && canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      const img = new Image()
      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx!.fillStyle = backgroundColor
        ctx!.fillRect(0, 0, canvas.width, canvas.height)
        ctx!.drawImage(img, 0, 0)
      }
      img.src = imageData
    }
  }, [imageData, backgroundColor])

  const handleSave = () => {
    if (canvasRef.current) {
      const link = document.createElement('a')
      link.download = `${handle}-bluesky-circlr.png`
      link.href = canvasRef.current.toDataURL()
      link.click()
    }
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>BlueSky Circle Generator</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="handle">BlueSky Handle</Label>
              <Input
                id="handle"
                value={handle}
                onChange={(e) => setHandle(e.target.value)}
                onBlur={(e) => {
                  // remove @ from handle
                  setHandle(e.target.value.replace('@', ''))
                  // remove invalid characters
                  setHandle(e.target.value.replace(/[^a-zA-Z0-9_\-.]/g, ''))
                }}
                pattern='@{0,1}[a-zA-Z0-9_\-.]*'
                placeholder="Enter BlueSky Handle"
                required
              />
            </div>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? loadingText : 'Generate Image'}
            </Button>
            {/* <Turnstile
              sitekey="1x00000000000000000000AA"
              onVerify={(token) => {
                setCaptchaKey(token)
              }}
            /> */}
          </form>
          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          {imageData && (
            <div className="mt-4 space-y-4">
              <div className="relative aspect-square w-full">
                <canvas
                  ref={canvasRef}
                  className="absolute inset-0 w-full h-full"
                />
              </div>
            </div>
          )}
        </CardContent>
        {imageData && (
          <CardFooter>
            <div className="flex w-full max-w-sm items-center space-x-2">
              <Input
                id="backgroundColor"
                type="color"
                value={backgroundColor}
                className="color-input"
                onChange={(e) => setBackgroundColor(e.target.value)}
              />
              <Button onClick={handleSave}>
                Save Image
              </Button>
            </div>
          </CardFooter>
        )}
        <footer className="mt-8 text-sm text-gray-500 space-y-1">
          <div className="flex items-center justify-center space-x-4">
            <a href="https://github.com/sparrowhe/bluesky-circle" className="flex items-center text-primary hover:text-primary/60 transition-colors">
              <Github className="w-4 h-4 mr-1" />
              Source Code
            </a>
            <a href="https://github.com/users/sparrowhe/projects/1" className="flex items-center text-primary hover:text-primary/60 transition-colors">
              <ExternalLink className="w-4 h-4 mr-1" />
              Roadmap
            </a>
          </div>
          <p className="text-center pb-2">
            Designed and developed by <a href="https://bsky.app/profile/sparrow.0x0e.top">SparrowHe</a> with ❤️
          </p>
        </footer>
      </Card>
    </div>
  )
}
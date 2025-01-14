export interface Article {
  id: string;
  title: string;
  source: string;
  sourceIcon: string;
  url: string;
  content: string;
}

export interface NewsItem {
  id: string;
  title: string;
  date: string;
  sources: string[];
  labels: string[];
  coverImage: string;
  description: string;
  summary: string;
  articles: Article[];
}

export const mockNews: NewsItem[] = [
  {
    id: '1',
    title: 'New AI Breakthrough in Natural Language Processing',
    date: '2023-05-15',
    sources: ['TechCrunch', 'Wired', 'MIT Technology Review'],
    labels: ['Technology', 'AI', 'Research'],
    coverImage: '/placeholder.svg?height=200&width=400',
    description: 'Researchers have developed a new AI model that significantly improves natural language understanding and generation.',
    summary: 'A team of researchers from leading tech companies and universities has announced a breakthrough in natural language processing. The new AI model, named "LinguaNet", demonstrates unprecedented accuracy in understanding context and nuance in human language, potentially revolutionizing applications such as machine translation, chatbots, and voice assistants.',
    articles: [
      {
        id: 'tc1',
        title: 'LinguaNet: The Next Big Thing in AI Language Models',
        source: 'TechCrunch',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://techcrunch.com/linguanet',
        content: `In a groundbreaking development, researchers have unveiled LinguaNet, a new AI language model that promises to revolutionize natural language processing. This cutting-edge technology demonstrates an unprecedented ability to understand and generate human-like text, potentially transforming various applications from chatbots to machine translation.

        Key features of LinguaNet include:
        1. Enhanced contextual understanding
        2. Improved sentiment analysis
        3. Multilingual capabilities
        4. Reduced bias compared to previous models

        Industry experts are hailing LinguaNet as a significant leap forward in AI technology, with potential applications across numerous sectors including customer service, content creation, and data analysis. As development continues, we can expect to see LinguaNet integrated into a wide range of products and services in the near future.`
      },
      {
        id: 'w1',
        title: 'How LinguaNet is Changing the Game for NLP',
        source: 'Wired',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://wired.com/linguanet-nlp',
        content: `LinguaNet, the latest breakthrough in natural language processing (NLP), is set to redefine how machines understand and generate human language. This innovative AI model, developed by a collaborative team of researchers from top tech companies and universities, showcases remarkable improvements in contextual understanding and nuanced communication.

        Unlike its predecessors, LinguaNet excels in:
        1. Grasping complex linguistic structures
        2. Interpreting idiomatic expressions
        3. Maintaining coherence in long-form text generation
        4. Adapting to various writing styles and tones

        The implications of LinguaNet's capabilities are far-reaching. From more natural-sounding virtual assistants to more accurate language translation services, the potential applications span across multiple industries. As LinguaNet continues to evolve, we may be witnessing the dawn of a new era in human-machine communication.`
      },
      {
        id: 'mit1',
        title: 'Breaking Down the Science Behind LinguaNet',
        source: 'MIT Technology Review',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://www.technologyreview.com/linguanet-science',
        content: `LinguaNet, the latest advancement in natural language processing, represents a significant leap forward in AI language models. This article delves into the technical innovations that power LinguaNet's impressive capabilities.

        At its core, LinguaNet utilizes a novel architecture that combines:
        1. Transformer-based deep learning
        2. Reinforcement learning techniques
        3. Unsupervised pre-training on diverse multilingual datasets
        4. Fine-tuning with human feedback

        One of the key breakthroughs is LinguaNet's ability to form more robust semantic representations, allowing it to capture subtle nuances in language that previous models struggled with. Additionally, its multilingual training approach enables zero-shot translation between languages, even for language pairs it wasn't explicitly trained on.

        The ethical considerations in LinguaNet's development are also noteworthy. The team implemented advanced debiasing techniques and rigorous testing to mitigate potential biases in the model's outputs. While challenges remain, LinguaNet represents a significant step towards more responsible and capable AI language models.`
      }
    ]
  },
  {
    id: '2',
    title: 'Global Climate Summit Reaches Landmark Agreement',
    date: '2023-05-14',
    sources: ['BBC', 'The Guardian', 'New York Times'],
    labels: ['Environment', 'Politics', 'Climate Change'],
    coverImage: '/placeholder.svg?height=200&width=400',
    description: 'World leaders have agreed on ambitious new targets to reduce carbon emissions and combat climate change.',
    summary: 'The recent Global Climate Summit concluded with a landmark agreement, committing participating nations to significant reductions in greenhouse gas emissions.  The agreement includes provisions for financial assistance to developing countries and a strengthened monitoring framework to ensure accountability.',
    articles: [
      {
        id: 'bbc1',
        title: 'Climate Summit: Historic Deal Reached',
        source: 'BBC',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://bbc.com/climate-summit',
        content: ''
      },
      {
        id: 'guardian1',
        title: 'Global Climate Accord: A Step Forward, But Challenges Remain',
        source: 'The Guardian',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://theguardian.com/climate-accord',
        content: ''
      },
      {
        id: 'nyt1',
        title: 'World Leaders Agree on Ambitious Climate Targets',
        source: 'New York Times',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://nytimes.com/climate-targets',
        content: ''
      }
    ]
  },
  {
    id: '3',
    title: 'SpaceX Successfully Launches Satellite Internet Constellation',
    date: '2023-05-13',
    sources: ['Space.com', 'NASA', 'CNBC'],
    labels: ['Space', 'Technology', 'Business'],
    coverImage: '/placeholder.svg?height=200&width=400',
    description: 'SpaceX has deployed another batch of Starlink satellites, bringing high-speed internet to remote areas.',
    summary: 'SpaceX successfully launched another large batch of Starlink satellites into orbit, expanding its global satellite internet constellation. This deployment marks a significant step towards providing high-speed internet access to underserved and remote regions worldwide.',
    articles: [
      {
        id: 'space1',
        title: 'SpaceX Expands Starlink Constellation',
        source: 'Space.com',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://space.com/starlink-launch',
        content: ''
      },
      {
        id: 'nasa1',
        title: 'NASA Monitors SpaceX Starlink Deployment',
        source: 'NASA',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://nasa.gov/starlink-monitoring',
        content: ''
      },
      {
        id: 'cnbc1',
        title: 'SpaceX\'s Starlink: A Booming Business in Space',
        source: 'CNBC',
        sourceIcon: '/placeholder.svg?height=32&width=32',
        url: 'https://cnbc.com/starlink-business',
        content: ''
      }
    ]
  }
];


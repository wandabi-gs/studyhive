from django.shortcuts import render
from agora.views import Agora

def Home(request):
    data = [
        {
            "index" : "odd",
            "title": 'Personalised Recommendation',
            "description": 'Receive a curated stream of articles, videos, and images tailored to your specific areas of study and interests. Enhance your learning experience with content personalized just for you.',
        },
        {
            "index" : "even",
            "title": 'Filtering Fake Content',
            "description": 'This platform leverages advanced machine learning algorithms to filter out offensive and inappropriate content. Additionally, it identifies potential misinformation, ensuring a safe and trustworthy environment for learning.',
        },
        {
            "index" : "odd",
            "title": 'Group Discussions',
            "description": 'Engage in meaningful group discussions with like-minded individuals. Participate in conversations related to your areas of interest and collaborate with others to deepen your understanding of various topics.',
        },
        {
            "index" : "even",
            "title": 'Group Chats',
            "description": 'Connect with fellow students in real-time through our group chat  "feature. Whether it\'s discussing project ideas, sharing insights, or seeking help, our chat system facilitates seamless communication among users.',
        },
        {
            "index" : "odd",
            "title": 'Upload Custom Content',
            "description": 'Contribute to the community by sharing your own articles, images, and videos. Showcase your knowledge and expertise while helping others discover valuable content in your chosen areas of study.',
        }
    ]
    
    return render(request=request, template_name='home.html', context={"features":data})
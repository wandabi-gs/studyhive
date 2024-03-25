import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from interest.models import UserReview, Recommendation, UserInterest, Interest
from user.models import Connection, CustomUser

def get_interest_recommendations(user: CustomUser) -> list[Recommendation]:
    # Retrieve user reviews, including reviews from connections
    user_reviews = pd.DataFrame.from_records(
        UserReview.objects.filter(user=user).values('user', 'recommendation__uid', 'like', 'dislike')
    )

    connection_reviews = pd.DataFrame.from_records(
        UserReview.objects.filter(
            user__uid__in=Connection.objects.filter(connection_status='accepted').values_list('connection__uid', flat=True)
        ).values('user', 'recommendation__uid', 'like', 'dislike')
    )

    combined_data = pd.concat([user_reviews, connection_reviews])

    # If there are no reviews, include recommendations based on interests of connections
    if combined_data.empty:
        connection_interests = pd.DataFrame.from_records(
            UserInterest.objects.filter(user__uid__in=Connection.objects.filter(connection_status='accepted').values_list('connection__uid', flat=True)).values('user__uid', 'interests__uid')
        )

        if connection_interests.empty:
            return []

        # Create user profile features based on interests of connections
        combined_data = pd.DataFrame(columns=['user', 'recommendation__uid', 'like', 'dislike'])
        combined_data['user'] = connection_interests['user__uid']
        combined_data['recommendation__uid'] = connection_interests['interests__uid']
        combined_data['like'] = False
        combined_data['dislike'] = False

    # Create user profile features based on likes and dislikes
    combined_data['user_like_count'] = combined_data['like'].astype(int) if 'like' in combined_data else 0
    combined_data['user_dislike_count'] = combined_data['dislike'].astype(int) if 'dislike' in combined_data else 0

    features = ['user_like_count', 'user_dislike_count']

    sparse_data = csr_matrix(combined_data[features])

    # Use NearestNeighbors for collaborative filtering
    recommender = NearestNeighbors(metric='cosine', algorithm='brute')
    recommender.fit(sparse_data)

    # Get the user profile for the current user
    user_profile = combined_data[combined_data['user'] == user.id][features]

    if len(user_profile) <= 0:
        return []

    k_neighbors = 5 if len(user_profile) > 5 else len(user_profile)

    sparse_user_profile = csr_matrix(user_profile)

    # Find k-nearest neighbors based on user profile
    distances, indices = recommender.kneighbors(sparse_user_profile, n_neighbors=k_neighbors)

    # Get recommended recommendations based on neighbors
    recommended_recommendations = Recommendation.objects.filter(
        uid__in=combined_data.iloc[indices[0, 1:]]['recommendation__uid'].values
    )

    return recommended_recommendations
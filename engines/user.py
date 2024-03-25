import pandas as pd
from django.db.models import Q
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from user.models import Connection, CustomUser as User, ReportedUser


def get_user_recommendations(authuser: User) -> list[User]:
    reported_users = list(ReportedUser.objects.filter(
        banned=True).values("user__uid"))

    user_connections = Connection.objects.filter(
        ~Q(connection_status='revoked'),
        (Q(user=authuser) | Q(connection=authuser))
    ).values_list('connection__uid', flat=True)

    user_connections = list(user_connections)

    user_connections_2 = Connection.objects.filter(
        ~Q(connection_status='revoked'),
        (Q(user=authuser) | Q(connection=authuser))
    ).values_list('user__uid', flat=True)

    user_connections_2 = list(user_connections_2)

    user_connections.extend(user_connections_2)

    user_connections = list(set(user_connections))

    possible_users = User.objects.filter(
        is_staff=False
    ).exclude(
        uid=authuser.uid
    ).exclude(
        uid__in=reported_users
    ).exclude(
        uid__in=user_connections
    ).distinct()

    if len(user_connections) > 1000:
        users_data = pd.DataFrame.from_records(
            User.objects.filter(uid__in=user_connections).values('uid', 'email')
        )

        vectorizer = TfidfVectorizer()
        user_emails = users_data['email'].astype(str)
        email_vectors = vectorizer.fit_transform(user_emails)

        recommender = NearestNeighbors(metric='cosine', algorithm='brute')
        recommender.fit(email_vectors)

        # Get the number of samples used for fitting the model
        n_samples = email_vectors.shape[0]

        # Convert the email of the authenticated user to a vector
        user_email_vector = vectorizer.transform([str(authuser.email)])

        _, indices = recommender.kneighbors(
            user_email_vector, n_neighbors=n_samples)

        # Convert indices to regular integers
        indices = indices.astype(int)
        indices = indices.flatten()

        possible_users = [possible_users[int(index)] for index in indices]

    return possible_users

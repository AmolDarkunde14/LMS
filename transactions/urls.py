from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowTransactionViewSet, IssueBookView, ReturnBookView

router = DefaultRouter()
router.register(r'history', BorrowTransactionViewSet, basename='transaction-history')

urlpatterns = [
    path('issue/', IssueBookView.as_view(), name='issue-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('', include(router.urls)),
]

from rest_framework import serializers
from ..models import Problem

class AdminProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'problem_ID', 'title', 'pdf', 'checker', 'test_cases', 'time_limit', 'memory_limit']

class UserProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'problem_ID', 'title', 'pdf', 'time_limit', 'memory_limit']

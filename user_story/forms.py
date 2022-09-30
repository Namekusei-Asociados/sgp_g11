from django.forms import ModelForm

from user_story.models import UserStory


class UserStoryForm(ModelForm):
    class Meta:
        model: UserStory
        fields: ['title', 'description', 'business_value', 'technical_priority', 'estimation_time', 'project']

from django.contrib import admin
from .models import Disc_Questions_Dataset, Disc_Score_Calculation_Dataset, NVI_Questions_Dataset

# Custom admin class for Disc_Questions_Dataset
class DiscQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('DISC_PROFILE_ID', 'QUESTION', 'A', 'B', 'C', 'D')

# Custom admin class for Disc_Score_Calculation_Dataset
class DiscScoreCalculationDatasetAdmin(admin.ModelAdmin):
    list_display = ('DISC_PROFILE_ID', 'D', 'I', 'S', 'C')

# Custom admin class for NVI_Questions_Dataset
class NVIQuestionsDatasetAdmin(admin.ModelAdmin):
    list_display = ('IMAGE_ID', 'IMAGE', 'OPTION1', 'OPTION2', 'OPTION3', 'OPTION4', 'OPTION5', 'OPTION6', 'OPTION7', 'OPTION8', 'ANSWERS')

# Register the models with the custom admin classes
admin.site.register(Disc_Questions_Dataset, DiscQuestionsDatasetAdmin)
admin.site.register(Disc_Score_Calculation_Dataset, DiscScoreCalculationDatasetAdmin)
admin.site.register(NVI_Questions_Dataset, NVIQuestionsDatasetAdmin)

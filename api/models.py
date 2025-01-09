from django.db import models

class Letter(models.Model):
    letter = models.CharField(max_length=1, unique=True)  # Single character (e.g., 'a', 'b', etc.)
    
    def __str__(self):
        return self.letter

    def image_count(self):
        return self.images.count()  


class LetterImage(models.Model):
    letter = models.ForeignKey(Letter, related_name='images', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='alphabet_images/')  
    is_correct = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.letter.letter} - {'Correct' if self.is_correct else 'Incorrect'}"
    

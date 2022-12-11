from django.db import models
from SS.settings import AUTH_USER_MODEL
from django.utils import timezone

# Create your models here.


class Gatherings(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()

    Moim = "모임"
    Study = "스터디"
    CATEGORIES = [
        (None, "모집유형을 선택해주세요."),
        (Moim, "모임"),
        (Study, "스터디"),
    ]

    category = models.CharField(
        choices=CATEGORIES, max_length=10, default="모집유형을 선택해주세요."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_gathering")
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    q = models.CharField(max_length=50, default="모임")

    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(gathering=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        dic = []
        cnt = 0
        for choice in self.choice_set.all():
            d = {}
            d["title"] = choice.choice_text
            d["num_votes"] = choice.get_vote_count
            d["pk"] = choice.pk
            if choice.vote_set.all():
                for i in choice.vote_set.all():
                    print(cnt)
                    d[str(cnt)] = i
                    cnt += 1

                    
            if not self.get_vote_count:
                d["percentage"] = 0
            else:
                d["percentage"] = (choice.get_vote_count / self.get_vote_count) * 100

            res.append(d)
        dic.append(res)
        return res

    def get_result_first(self):
        result = []
        for choice in self.choice_set.all():
            d = {}
            d["title"] = choice.choice_text
            d["num_votes"] = choice.get_vote_count

            result.append(d)
        result = sorted(result, key=lambda x: x["num_votes"], reverse=True)
        max = result[0]["num_votes"]

        title = []
        for res in result:
            if res["num_votes"] == max:
                title.append(res["title"])

        return title

    def __str__(self):
        return self.title


class GatheringsComment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    gathering = models.ForeignKey(
        Gatherings, on_delete=models.CASCADE, related_name="gatheringcomments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReComment3(models.Model):
    comment = models.ForeignKey(
        GatheringsComment,
        on_delete=models.CASCADE,
        related_name="gatherings_comment_user",
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField("답글", max_length=200)
    updated_at = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    gathering = models.ForeignKey(Gatherings, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.gathering.title[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    gathering = models.ForeignKey(Gatherings, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

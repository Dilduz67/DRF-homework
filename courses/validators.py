from rest_framework import serializers


class LinksValidator:
    def __init__(self,link_str):
        self.link = link_str

    def __call__(self, value):
        tmp_val=dict(value).get(self.link)
        if tmp_val and 'youtube.com' not in tmp_val:
            raise serializers.ValidationError('Ссылка возможно только на youtube.com')
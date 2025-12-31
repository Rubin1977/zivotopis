from unittest.mock import Mock, patch
from zivotopis.utils import save_post_with_images

@patch("zivotopis.models.Image")
def test_save_post_with_images(mock_image):
    form = Mock()
    post = Mock()
    form.save.return_value = post

    user = Mock()
    files = ["img1.jpg", "img2.jpg"]

    result = save_post_with_images(form, user, files)

    assert result == post
    assert post.author == user
    assert mock_image.objects.create.call_count == 2

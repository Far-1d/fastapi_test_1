import pytest

def test_get_posts(authorized_user, create_posts):
    res = authorized_user.get("/posts")
    print(res.json())
    assert res.status_code == 200


def test_get_posts_unauthorized(client, create_posts, post_id):

    res =client.delete(f"/posts/{post_id.id}")
    #print(res.json())
    assert res.status_code == 401

# this test gives 401_UNAUTHORIZED instead of 404_NOT_FOUND
#find the problem
def test_delete_nan_posts_authorized(authorized_user, create_posts):

    res = authorized_user.delete("/posts/1")
    #print(res.json())
    assert res.status_code == 404

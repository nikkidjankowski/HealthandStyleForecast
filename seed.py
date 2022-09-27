from app import app
from models import Users, HealthIssues, Forecasts, Outfits, Locations, db, connect_db

db.drop_all()
db.create_all()

u1 = Users(
    username ="nikkij",
    password = "12345",
    email ="nikkij@email.com",
    first_name = "nikki",
    last_name = "jankowski",
    )

l1 = Locations(
    address="San Diego, CA",
    username="nikkij",
)
 {% for i in currenthealth %}

    <table class="move">
      <th class="test">Whatt to look out for in {{ i[0] }}</th>
      <tr>
      <td>{{ i[1] }} {{ i[2] }}</td>
      </tr>
    </table>
    {% endfor %} 

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")
@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")

{% extends 'base.html' %}

{% block title %}Edit Post{% endblock %}

{% block content %}

<h1>Edit Post</h1>

<form method="POST" action="/posts/{{ post.id }}/edit">

  <div class="form-group row">
    <label for="title" class="col-sm-2 col-form-label">Title</label>
    <div class="col-sm-10">
      <input class="form-control" id="title" name="title" value="{{ post.title }}">
    </div>
  </div>

  <div class="form-group row">
    <label for="content" class="col-sm-2 col-form-label">Post Content</label>
    <div class="col-sm-10">
      <textarea class="form-control"
                id="content"
                name="content">{{ post.content }}</textarea>
    </div>
  </div>

  <div class="form-check">
    {% for tag in tags %}
    <div>
      <input class="form-check-input"
             type="checkbox"
             value="{{ tag.id }}"
             id="tag_{{ tag.id }}"
             {% if tag in post.tags %}checked{% endif %}
             name="tags">
      <label class="form-check-label" for="tag_{{ tag.id }}">
        {{ tag.name }}
      </label>
    </div>
    {% endfor %}
  </div>

  <div class="form-group row">
    <div class="ml-auto mr-3">
      <a href="/users/{{ post.user_id }}" class="btn btn-outline-info">
        Cancel
      </a>
      <button type="submit" class="btn btn-success">
        Edit
      </button>
    </div>
  </div>

</form>

{% endblock %}








    def setup_likes(self):
        m1 = Message(text="trending warble", user_id=self.testuser_id)
        m2 = Message(text="Eating some lunch", user_id=self.testuser_id)
        m3 = Message(id=9876, text="likable warble", user_id=self.u1_id)
        db.session.add_all([m1, m2, m3])
        db.session.commit()

        l1 = Likes(user_id=self.testuser_id, message_id=9876)

        db.session.add(l1)
        db.session.commit()
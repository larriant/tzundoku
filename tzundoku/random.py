if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first() 
        if form.validate() == False:
            return render_template('item.html', item=item, showitems=showitems, form=form, form2=form2)
        else:
            post = Post(user.id, form.message.data, datetime.datetime.utcnow(), itemid)
            db.session.add(post)
            db.session.commit()
            flash('You have added a post!')
            return redirect(url_for('item', id=itemid)) 

    elif request.method == 'GET':
        return render_template('item.html', item=item, showposts=showposts, form=form, form2=form2)
    


from twitoff.models import DB, User, Tweet

DB.create_all()
u1 = User(name='donaldtrump')
u2 = User(name='elonmusk')
t1 = Tweet(text="Healthy young child goes to doctor, gets pumped with massive shot of many vaccines, doesn’t feel good and changes – AUTISM. Many such cases!")
t2 = Tweet(text="Sorry losers and haters, but my I.Q. is one of the highest -and you all know it! Please don’t feel so stupid or insecure,it’s not your fault")
t3 = Tweet(text="Windmills are the greatest threat in the US to both bald and golden eagles. Media claims fictional ‘global warming’ is worse.")
t4 = Tweet(text="When the zombie apocalypse happens, you’ll be glad you bought a flamethrower. Works against hordes of the undead or your money back!")
t5 = Tweet(text="Why is there no Flat Mars Society!?")
t6 = Tweet(text="The rumor that I'm building a spaceship to get back to my home planet Mars is totally untrue")
u1.tweets.append(t1)
u1.tweets.append(t2)
u1.tweets.append(t3)
u2.tweets.append(t4)
u2.tweets.append(t5)
u2.tweets.append(t6)
DB.session.add(u1)
DB.session.add(u2)
DB.session.commit()

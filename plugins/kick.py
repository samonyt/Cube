import discord
# Imports go here.

async def kick(app):
    if app.args == []:
        embed=discord.Embed(title="No user found.", description="Please provide the user and the kick reason as arguments.", color=0xff0000)
        embed.set_footer(text=app.premade_ver)
        await app.say(embed=embed)
    else:
        user = app.pass_user(app.args[0], app.message.server)
        if user is None:
            embed=discord.Embed(title="User not found.", description="Please make sure you give the user as the first argument and they are a valid user.", color=0xff0000)
            embed.set_footer(text=app.premade_ver)
            await app.say(embed=embed)
        else:
            if len(app.args) == 1:
                reason = "No reason found."
            else:
                del app.args[0]
                reason = ' '.join(app.args)
            await app.say("Are you sure you want to kick `{}` for `{}`? Please say yes in order to run this action.".format(user.name, reason))
            msg2 = await app.dclient.wait_for_message(author=app.message.author, timeout=30)
            if msg2 is None or not "yes" in msg2.content.lower():
                await app.say("Kick cancelled.")
            else:
                try:
                    await app.dclient.kick(user)
                    sql = "INSERT INTO kicks(user_id, staff_id, server_id, reason) VALUES(%s, %s, %s, %s)"
                    with app.mysql_connection.cursor() as cursor:
                        cursor.execute(sql, (user.id, app.message.author.id, app.message.server.id, reason, ))
                        cursor.close()
                    generic_desc = "`{}` has been kicked for `{}`".format(user.name, reason)
                    embed=discord.Embed(title="User kicked:", description="{}.".format(generic_desc), color=0xff0000)
                    embed.set_footer(text=app.premade_ver)
                    await app.say(embed=embed)
                    log_embed=discord.Embed(title="User kicked:", description="{} by `{}`.".format(generic_desc, app.message.author.name))
                    await app.attempt_log(app.message.server.id, log_embed)
                except:
                    await app.say("Could not kick the specified user.")
# Allows you to kick users.

kick.description = "Allows you to kick users."
# Sets a description for "kick".

kick.requires_staff = True
# Set that this script requires staff.

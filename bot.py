import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

MODERATION_LOG_CHANNEL_ID = "ID" # - Без кавычек
MESSAGE_LOG_CHANNEL_ID = "ID" # - Без кавычек

async def log_action(title, description):
    log_channel = bot.get_channel(MODERATION_LOG_CHANNEL_ID)
    embed = disnake.Embed(
        title=title,
        description=description,
        color=disnake.Color.blue()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_create(role):
    audit_logs = await role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_create).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Создана роль: {role.name}\nСоздатель: {issuer.mention}"
        await log_action("Роль создана", description)

@bot.event
async def on_guild_role_delete(role):
    audit_logs = await role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Удалена роль: {role.name}\nУдаливший: {issuer.mention}"
        await log_action("Роль удалена", description)

@bot.event
async def on_guild_role_update(before, after):
    audit_logs = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Изменена роль: {before.name}\nИзменивший: {issuer.mention}"
        
        # Проверка изменения имени роли
        if before.name != after.name:
            description += f"\nСтарое имя: {before.name}\nНовое имя: {after.name}"
        
        await log_action("Роль изменена", description)

# Логирование изменений каналов
@bot.event
async def on_guild_channel_create(channel):
    audit_logs = await channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Создан канал: {channel.name}\nСоздатель: {issuer.mention}"
        await log_action("Канал создан", description)

@bot.event
async def on_guild_channel_delete(channel):
    audit_logs = await channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Удалён канал: {channel.name}\nУдаливший: {issuer.mention}"
        await log_action("Канал удалён", description)

@bot.event
async def on_guild_channel_update(before, after):
    audit_logs = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_update).flatten()
    if audit_logs:
        issuer = audit_logs[0].user
        description = f"Изменён канал: {before.name}\nИзменивший: {issuer.mention}"
        await log_action("Канал изменён", description)


@bot.event
async def on_member_update(before, after):

    added_roles = [role for role in after.roles if role not in before.roles]
    if added_roles:
        for role in added_roles:
            audit_logs = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update).flatten()
            if audit_logs:
                issuer = audit_logs[0].user
                description = f"Участник: {after.mention}\nВыдана роль: {role.name}\nВыдавший: {issuer.mention}"
                await log_action("Роль выдана", description)


    removed_roles = [role for role in before.roles if role not in after.roles]
    if removed_roles:
        for role in removed_roles:
            audit_logs = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update).flatten()
            if audit_logs:
                issuer = audit_logs[0].user
                description = f"Участник: {after.mention}\nРоль убрана: {role.name}\nУдалил: {issuer.mention}"
                await log_action("Роль убрана", description)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
    embed = disnake.Embed(
        title="Сообщение было удалено",
        color=disnake.Color.red()
    )
    embed.add_field(name="Удалённое сообщение:", value=f"```{message.content}```", inline=False)
    embed.add_field(name="Автор:", value=message.author.mention, inline=False)
    embed.add_field(name="Канал:", value=message.channel.mention, inline=False)
    embed.add_field(name="Дата и время:", value=message.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    log_channel = bot.get_channel(MESSAGE_LOG_CHANNEL_ID)
    embed = disnake.Embed(
        title="Сообщение было отредактировано",
        color=disnake.Color.blue()
    )
    embed.add_field(name="Старое содержимое:", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Новое содержимое:", value=f"```{after.content}```", inline=False)
    embed.add_field(name="Автор:", value=before.author.mention, inline=False)
    embed.add_field(name="Канал:", value=before.channel.mention, inline=False)
    embed.add_field(name="Дата и время:", value=before.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    await log_channel.send(embed=embed)

bot.run(token)

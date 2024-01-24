from interactions.models.internal.extension import Extension
from interactions import slash_command, SlashContext, Modal, ShortText, ParagraphText, ModalContext, Color
import nosync_tools as ns
import datetime



class maintain_bugs(Extension):

    @slash_command(name="report_bug", description="Report a bug to the Bot Owner")
    async def bug_report_backend(self, ctx: SlashContext):
        bug_modal= Modal(ShortText(label="Title", custom_id="bug_title", placeholder="Shortly name the issue you are facing"), ParagraphText(label="Description of your Issue", custom_id="bug_description", placeholder="Describe your issue in as much detail as possible"), title="Bug Report")
        await ctx.send_modal(modal=bug_modal)
        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(bug_modal)
        print()
        bug_structure = [f"Reporter: {modal_ctx.author.display_name}", f"Title:\n{modal_ctx.responses['bug_title']}", f"Description:\n{modal_ctx.responses['bug_description']}", f"Time: [{datetime.datetime.now()}]", "#################################################"]
        with open("Bugreports.txt", "a") as f: # sorts different bug report sections
            for i in bug_structure:
                f.write(i)
                f.write("\n")
        ns.logthis("warning", f"New Bug Report Submitted by {ctx.author.display_name}")
        await modal_ctx.send("Your Bug Report was successfully sent", ephemeral=True, color=Color.GREEN)

def setup(bot):
    maintain_bugs(bot)
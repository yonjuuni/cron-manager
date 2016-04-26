from flask import Flask, render_template, flash, request
from db_connect import db_add, db_delete
import main as m


app = Flask('cron-manager')
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    info = m.get_sys_info()

    if request.method == 'POST':
        # flash(request.form, 'info')

        if 'add' in request.form:
            try:
                cron = m.text_to_cron_object(request.form.get('cron'))
                db_add(cron)
            except:
                flash("Bad entry. Validation not implemented, so try again.",
                      'danger')
            else:
                cron_db_list = m.get_cron_list()
                m.create_crontab_file()
                flash('"{}" was added'.format(cron.output()), 'success')

        elif 'sync' in request.form:
            try:
                m.create_crontab_file()
                m.write_crontab()
            except Exception as e:
                flash("There's been an error: " + e, 'danger')
            else:
                cron_list = m.read_crontab(from_file=False)
                flash('Stuff got synced!', 'success')

        elif 'del' in request.form:
            try:
                db_delete(request.form.get('del'))
            except Exception as e:
                flash("Unable to proceed. Details: " + e, 'danger')
            else:
                cron_db_list = m.get_cron_list()
                m.create_crontab_file()
                flash("Successfully removed.", 'success')

    cron_list = m.read_crontab()
    cron_file_list = m.read_crontab(from_file=True)
    cron_db_list = m.get_cron_list()
    # flash(cron_list, 'info')
    # flash(cron_file_list, 'info')

    if (not(cron_list and cron_file_list) or
        ([c.output() for c in cron_list] !=
            [c.output() for c in cron_file_list])):
        flash('System crontab is outdated', 'warning')

    if not cron_list:
        flash("System crontab is empty", 'info')
    if not cron_db_list:
        flash('DB is empty', 'info')

    return render_template('index.html',
                           system=info[0],
                           user=info[1],
                           cron_raw=cron_list,
                           cron_db=cron_db_list)


if __name__ == '__main__':
    app.run()

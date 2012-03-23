# -*- coding: utf-8 -*-

import unittest
from bakatest import ok, prepare, topic, spec, fixture
prepare()

from markupsafe import Markup, escape
from formhelper import Form, FormHelper, checked, selected, disabled


with topic('Form'):


    with topic('#__init__()'):

        @spec("takes param dict.")
        def _(self):
            params = {'team': 'SOS'}
            form = Form(params)
            ok (form.params).is_(params)

        @spec("creates errors dict.")
        def _(self):
            form = Form({})
            ok (form.errors).is_a(dict).length(0)


    with topic('#validate()'):

        @spec("is abstract method.")
        def _(self):
            form = Form({})
            def fn(): form.validate()
            ok (fn).raise_(NotImplementedError)


class HelloForm(Form):

    def validate(self):
        k = 'name'
        v = self.params.get(k, '').strip()
        if not v:
            self.errors[k] = 'Required.'
        elif len(v) > 100:
            self.errors[k] = 'Too long (max 100 chars).'


with topic('FormHelper'):


    with topic('#__init__()'):

        @spec("takes form object.")
        def _(self):
            form = Form({})
            fh = FormHelper(form)
            ok (fh._form).is_(form)


    @fixture
    def fx_valid_form(self):
        form = HelloForm({'name': 'Haruhi'})
        form.validate()
        return form

    @fixture
    def fx_invalid_form(self):
        form = HelloForm({'name': ''})
        form.validate()
        return form

    @fixture
    def fx_valid_form_helper(self, valid_form):
        return FormHelper(valid_form)

    @fixture
    def fx_invalid_form_helper(self, invalid_form):
        return FormHelper(invalid_form)


    with topic('#param()'):

        @spec("push/pop parameter name.")
        def _(self, valid_form_helper):
            fh = valid_form_helper
            with fh.param('name'):
                with fh.param('age'):
                    with fh.param('birthday'):
                        fh._param_stack == ['name', 'age', 'birthday']
                    fh._param_stack == ['name', 'age']
                fh._param_stack == ['name']
            fh._param_stack == []


    with topic('#ec()'):

        @spec("returns empty string when parameter has no error.")
        def _(self, valid_form_helper):
            fh = valid_form_helper
            ok (fh.ec('name')) == ''

        @spec("returns 'class=\"err-exist\"' when parameter has error.")
        def _(self, invalid_form_helper):
            fh = invalid_form_helper
            ok (fh.ec('name')) == Markup('class="err-exist"')


    with topic('#em()'):

        @spec("returns empty string when parameter has no error.")
        def _(self, valid_form_helper):
            fh = valid_form_helper
            ok (fh.em('name')) == ''

        @spec("returns '<em class=\"err-desc\">MESSAgE</em>' when parameter has error.")
        def _(self, invalid_form_helper):
            fh = invalid_form_helper
            errmsg = invalid_form_helper._form.errors.get('name')
            ok (errmsg) == 'Required.'
            ok (fh.em('name')) == Markup('<em class="err-desc">%s</em>' % errmsg)


    with topic('#nv()'):

        @spec("returns 'name=\"...\" value=\"...\"' string.")
        def _(self, valid_form_helper, invalid_form_helper):
            ok (  valid_form_helper.nv('name')) == Markup('name="name" value="Haruhi"')
            ok (invalid_form_helper.nv('name')) == Markup('name="name" value=""')



    with topic('#nvc()'):

        @spec("returns attributes without 'checked' when parameter is different from value.")
        def _(self, valid_form_helper, valid_form):
            valid_form.params['radio1'] = ''
            ok (valid_form_helper.nvc('radio1', 'val1')) == Markup('name="radio1" value="val1"')
            valid_form.params['radio1'] = 'xxx'
            ok (valid_form_helper.nvc('radio1', 'val1')) == Markup('name="radio1" value="val1"')

        @spec("returns attributes with 'checked' when parameter equals to value.")
        def _(self, valid_form_helper, valid_form):
            valid_form.params['radio2'] = 'val2'
            ok (valid_form_helper.nvc('radio2', 'val2')) == Markup('name="radio2" value="val2" checked="checked"')


with topic('<global>'):


    with topic('checked()'):

        @spec("returns empty string when argument is falthy value.")
        def _():
            ok (checked(1==0)) == ''

        @spec("returns 'checked=\"checked\"' when argument is truthy value.")
        def _():
            ok (checked(1==1)) == Markup('checked="checked"')


    with topic('selected()'):

        @spec("returns empty string when argument is falthy value.")
        def _():
            ok (selected(1==0)) == ''

        @spec("returns 'selected=\"selected\"' when argument is truthy value.")
        def _():
            ok (selected(1==1)) == Markup('selected="selected"')


    with topic('disabled()'):

        @spec("returns empty string when argument is falthy value.")
        def _():
            ok (disabled(1==0)) == ''

        @spec("returns 'disabled=\"disabled\"' when argument is truthy value.")
        def _():
            ok (disabled(1==1)) == Markup('disabled="disabled"')



if __name__ == '__main__':
    import bakatest
    bakatest.run()
jinja\_bs\_modal
================

Jinja extension for rendering Bootstrap modals.

Usage
-----

.. code:: jinja

    {% modal(id='modal-edit', title='Caption here', focus='[name=title]') %}
        Here goes modal body.
        <input type="text" name="title" value="This input will get focus on when modal activates">
    {% modal_footer %}
        It's optional, actually.
        <button type="button" data-dismiss="modal">Ok</button>
    {% endmodal %}

Configuring Jinja
-----------------

.. code:: python

    from jinja_bs_modal import JinjaBSModalExtension

    env = jinja2.Environment(extensions=[CompressorExtension])

Configuring Flask
-----------------

.. code:: python

    from jinja_bs_modal import JinjaBSModalExtension

    app = Flask(__name__)
    app.jinja_env.add_extension(JinjaBSModalExtension)


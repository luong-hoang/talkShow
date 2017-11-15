(function($) {
    var sl = {
        edit_link: '.edit_subject', edit_block: '.change', edit_cancel: '.cancel', edit_confirm: '.confirm',
        add_block: '.add_block'
    };
    var cl = {hide: 'd-none'};
    var endpoint = '';

    $(document).ready(function() {
        endpoint = $('input[name="endpoint"]').val();

        $(document).on('click', sl.edit_link, function(e) {
            e.preventDefault();
            $link = $(this);
            $change = $link.siblings(sl.edit_block);
            $link.addClass(cl.hide);
            $change.removeClass(cl.hide).focus();
        });

        // Enter to change subject
        $(document).on('keypress', sl.edit_block, function(e) {
            $change    = $(this);
            $list_item = $change.parents('li').first();
            $list      = $('ul');
            var key = e.keyCode;
            if (key === 13) {
                var id = $change.data('id');
                edit_subject_ajax($change.val(), id, function(data) {
                    if (data.is_new) {
                        $(sl.add_block).hide();
                        $list.append(data.content);
                    } else {
                        $list_item.replaceWith(data.content);
                    }
                });
            }
        });

        // Keypress not working for escape key
        $(document).on('keyup', sl.edit_block, function(e) {
            if (e.keyCode == 27) {
                cancel_edit($(this))
            }
        })
        $(document).on('blur', sl.edit_block, function() {
            cancel_edit($(this));
        });
    });

    function cancel_edit($element) {
        $link = $change.siblings(sl.edit_link);
        $change.addClass(cl.hide);
        $link.removeClass(cl.hide);
    }

    function edit_subject_ajax(subject, id, callback) {
        $.ajax({
            url: endpoint,
            dataType: 'json',
            method: 'POST',
            data: csrf_token({subject: subject, id: id}),
            success: function(result) {
                if (result.status) {
                    if (typeof(callback) === 'function') {
                        callback(result);
                    }
                } else {
                    alert(result.msg);
                }
            }
        });
    }

    function csrf_token(obj) {
        var key = 'csrfmiddlewaretoken';
        var value = $('input[name="' + key + '"]').val();
        obj[key] = value;
        return obj;
    }
})(jQuery)
$('#person-switcher').on('click', () => {
    // Hide acc
    $('#acc-setting-box').hide();
    $('#acc-switcher').css({
        backgroundColor: '#a1a6b3',
        // borderLeft: 'solid #6A6D75 1px',
    });

    // Show person
    $('#person-switcher').css({
        backgroundColor: '#FFFFFF',
        border: 'none',
    });
    $('#person-setting-box').show();

    // Hide forms
    $('#person-setting-form').hide();
    $('#acc-setting-form').hide();
})

$('#acc-switcher').on('click', () => {
    // Hide person
    $('#person-setting-box').hide();
    $('#person-switcher').css({
        backgroundColor: '#a1a6b3',
        // borderRight: 'solid #6A6D75 1px',
    });
    // Show acc
    $('#acc-switcher').css({
        backgroundColor: '#FFFFFF',
        border: 'none',
    });
    $('#acc-setting-box').show();

    // Hide form 
    $('#person-setting-form').hide();
    $('#acc-setting-form').hide();
});

// Show form when event fire
$('#change-person-info-button').on('click', () => {
    //show change person info form 
    $('#person-setting-form').show();
    $('#person-setting-box').hide();
})

$('#change-acc-info-button').on('click', () => {
    //show change acc info form 
    $('#acc-setting-form').show();
    $('#acc-setting-box').hide();
})

$('#person-switcher').click()
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
})

$('#person-switcher').click()
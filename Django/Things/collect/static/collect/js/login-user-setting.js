// $(document).load(() => {
//     $('#acc-setting-box').addClass('hidden-class');
// });

$('#person-switcher').on('click', () => {
    $('#person-setting-box').show();
    $('#acc-setting-box').hide()
})

$('#acc-switcher').on('click', () => {
    $('#person-setting-box').hide();
    $('#acc-setting-box').show()
})

$('#person-switcher').click()
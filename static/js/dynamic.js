/**
 * Created by Adelola on 24/12/2017.
 */



var msg = "";
var send_user = "";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

function send_msg(msg, send_user) {
    var date = formatAMPM(new Date());
    var send_msg = '<div class="row">' +
                        '<div class="messages msg_receive">' +
                            '<p>' + msg + '</p>' +
                            '<time>' + send_user + ' • ' +  date + '</time>' +
                        '</div>' +
               '</div>';

    $(".panel-body").append(send_msg);
    $(".panel-body").scrollTop($(".panel-body")[0].scrollHeight);
}
function receive_msg(msg, receive_user) {
    var date = formatAMPM(new Date());
    var send_user = 'michru';
    var send_msg = '<div class="row">' +
                        '<div class="messages msg_sent">' +
                            '<p>' + msg + '</p>' +
                            '<time>' + receive_user + ' • ' +  date + '</time>' +
                        '</div>' +
               '</div>';

    $(".panel-body").append(send_msg);
    $(".panel-body").scrollTop($(".panel-body")[0].scrollHeight);
}
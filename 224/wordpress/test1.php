<?php
// No need for the template engine
define( 'WP_USE_THEMES', false );
// Load WordPress Core
require_once( 'wp-load.php' );

$prepared_login = $wpdb->prepare("user_login = %s", $_GET['login']);
print_r( $prepared_login.PHP_EOL );
$prepared_sql = $wpdb->prepare("SELECT id, user_login, user_pass FROM $wpdb->users WHERE $prepared_login AND user_pass = %s", $_GET['pass']);
print_r( $prepared_sql.PHP_EOL );
var_dump( $wpdb->get_results( $prepared_sql ) );
<?php
// No need for the template engine
define( 'WP_USE_THEMES', false );
// Load WordPress Core
require_once( 'wp-load.php' );

$sql = "SELECT id, post_name, post_title, post_content FROM $wpdb->posts WHERE id = %d AND post_type = %s";
$prepared_sql = $wpdb->prepare( $sql, $_GET['id'], 'post' );
print_r( $prepared_sql.PHP_EOL );
var_dump( $wpdb->get_results( $prepared_sql ) );
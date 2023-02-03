/* Based on https://github.com/brandoncorbin/string_to_color */

var stringToTriColourPalatte = function (str) {
  // Generate a Hash for the String
  var hash = function (word) {
    var h = 0;
    for (var i = 0; i < word.length; i++) {
      h = word.charCodeAt(i) + ((h << 5) - h);
    }
    return h;
  };

  // Change the darkness or lightness
  var shade = function (color, prc) {
    var num = parseInt(color, 16),
      amt = Math.round(2.55 * prc),
      R = (num >> 16) + amt,
      G = ((num >> 8) & 0x00ff) + amt,
      B = (num & 0x0000ff) + amt;
    return (
      "#" +
      (
        0x1000000 +
        (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
        (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
        (B < 255 ? (B < 1 ? 0 : B) : 255)
      )
        .toString(16)
        .slice(1)
    );
  };

  // Convert hash to an RGBA
  var int_to_rgba = function (i) {
    var color =
      ((i >> 24) & 0xff).toString(16) +
      ((i >> 16) & 0xff).toString(16) +
      ((i >> 8) & 0xff).toString(16) +
      (i & 0xff).toString(16);
    return color;
  };

  var base_colour = int_to_rgba(hash(str));
  var colours = [
    shade(base_colour, 64),
    shade(base_colour, -64),
    shade(base_colour, -48),
  ];

  return colours;
};

export default stringToTriColourPalatte;

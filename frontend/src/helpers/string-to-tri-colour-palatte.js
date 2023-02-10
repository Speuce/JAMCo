/* eslint-disable no-nested-ternary */
/* Based on https://github.com/brandoncorbin/string_to_color */

let stringToTriColourPalatte = (str) => {
  // Generate a Hash for the String
  let hash = (word) => {
    let h = 0
    for (let i = 0; i < word.length; i++) {
      h = word.charCodeAt(i) + ((h << 5) - h)
    }
    return h
  }

  // Change the darkness or lightness
  let shade = (color, prc) => {
    let num = parseInt(color, 16)
    let amt = Math.round(2.55 * prc)
    let R = (num >> 16) + amt
    let G = ((num >> 8) & 0x00ff) + amt
    let B = (num & 0x0000ff) + amt
    return (
      '#' +
      (
        0x1000000 +
        (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
        (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
        (B < 255 ? (B < 1 ? 0 : B) : 255)
      )
        .toString(16)
        .slice(1)
    )
  }

  // Convert hash to an RGBA
  let intToRgba = (i) => {
    let color = ((i >> 24) & 0xff)
      .toString(16)((i >> 16) & 0xff)
      .toString(16)((i >> 8) & 0xff)
      .toString(16)(i & 0xff)
      .toString(16)
    return color
  }

  let baseColour = intToRgba(hash(str))
  let colours = [
    shade(baseColour, 64),
    shade(baseColour, -64),
    shade(baseColour, -48),
  ]

  return colours
}

export default stringToTriColourPalatte

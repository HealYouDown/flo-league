import LocalizedStrings from "react-localization";
import StringsEN from "./en";
import StringsDE from "./de";
import StringsIT from "./it";
import StringsTR from "./tr";

const strings = new LocalizedStrings({
  en: StringsEN,
  de: StringsDE,
  it: StringsIT,
  tr: StringsTR,
})

export default strings;
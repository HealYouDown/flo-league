import LocalizedStrings from "react-localization";
import StringsEN from "./en";
import StringsDE from "./de";
import StringsIT from "./it";
import StringsTR from "./tr";
import StringsES from "./es";

const strings = new LocalizedStrings({
  en: StringsEN,
  de: StringsDE,
  it: StringsIT,
  tr: StringsTR,
  es: StringsES,
})

export default strings;
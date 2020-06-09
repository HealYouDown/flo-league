import LocalizedStrings from "react-localization";
import StringsEN from "./en";
import StringsDE from "./de";
import StringsIT from "./it";

const strings = new LocalizedStrings({
  en: StringsEN,
  de: StringsDE,
  it: StringsIT,
})

export default strings;
import LocalizedStrings from "react-localization";
import StringsEN from "./en";
import StringsDE from "./de";

const strings = new LocalizedStrings({
  en: StringsEN,
  de: StringsDE,
})

export default strings;
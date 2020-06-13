import LocalizedStrings from "react-localization";
import StringsEN from "./en";
import StringsDE from "./de";
import StringsIT from "./it";
import StringsTR from "./tr";
import StringsES from "./es";
import StringsFR from "./fr";
import StringsPT from "./pt";

const strings = new LocalizedStrings({
  en: StringsEN,
  de: StringsDE,
  fr: StringsFR,
  it: StringsIT,
  tr: StringsTR,
  es: StringsES,
  pt: StringsPT,
})

export default strings;
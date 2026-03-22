interface PageLayoutProps extends React.PropsWithChildren {
  title?: string
}

export function PageLayout({ title, children }: PageLayoutProps) {
  return (
    <div className="container mx-auto p-4 flex flex-col gap-4">
      {title && (
        <>
          <h1 className="text-2xl font-semibold">{title}</h1>
          <hr />
        </>
      )}
      {children}
    </div>
  )
}

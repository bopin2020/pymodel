SHELL = pwsh
VERSION = v2.3

default: gitrelease
	pwsh -command Write-Host ""

gitrelease:
	git tag $(VERSION)
	git push origin $(VERSION)
	gh release create $(VERSION) --notes-file ".\doc\release-notes.md" --title "pymodel$(VERSION)"
	pwsh -command Compress-Archive . -DestinationPath pymodel$(VERSION).zip
	gh release upload $(VERSION) .\pymodel$(VERSION).zip
	pwsh -command Remove-Item pymodelv*.zip

clean:
	pwsh -command Remove-Item pymodelv*.zip
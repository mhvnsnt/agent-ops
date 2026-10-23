#!/usr/bin/env bash
# bk.sh <clone-dir> <name> — back up dirty/untracked files of a clone to SHA-verified Release assets in mhvnsnt/box-storage. See docs/END-OF-SESSION-BACKUP.md
set -u
d=$1; name=$2; tag=box-2026-10-14-final-$name; R=mhvnsnt/box-storage
cd $d
gh release view $tag -R $R >/dev/null 2>&1 || gh release create $tag -R $R --title "$tag" --notes "dirty/untracked backup of $d" >/dev/null
M=/dev/shm/manifest-$name.txt; : > $M
git status --porcelain -uall | while IFS= read -r l; do st=${l:0:2}; p=${l:3}
 if [ -f "$p" ]; then s=$(sha256sum "$p"|cut -d' ' -f1); a=$(echo "$p"|sed 's#/#__#g'); echo -e "$p\t$st\t$s\t$a" >> $M
 elif [ -d "$p" ]; then echo -e "$p\t$st\tDIR(gitlink $(git -C "$p" rev-parse HEAD 2>/dev/null))\t-" >> $M
 else echo -e "$p\t$st\tDELETED\t-" >> $M; fi; done
awk -F'\t' '$4!="-"{print $1"\t"$4}' $M | while IFS=$'\t' read p a; do gh release upload $tag -R $R --clobber "$p#$a" >/dev/null 2>&1 || { cp "$p" "/dev/shm/$a" && gh release upload $tag -R $R --clobber "/dev/shm/$a" >/dev/null && rm "/dev/shm/$a"; } || echo FAIL $p; done
cp $M /dev/shm/manifest.txt; gh release upload $tag -R $R --clobber /dev/shm/manifest.txt >/dev/null
gh api repos/$R/releases/tags/$tag --jq '.assets[]|[.name,.digest]|@tsv' > /dev/shm/dig-$name
ok=0; bad=0; while IFS=$'\t' read p st s a; do [ "$a" = - ] && continue; g=$(awk -F'\t' -v a="$a" '$1==a{print $2}' /dev/shm/dig-$name); [ "$g" = "sha256:$s" ] && ok=$((ok+1)) || { bad=$((bad+1)); echo "MISMATCH $p [$g]"; }; done < $M
echo "$name: verified=$ok bad=$bad entries=$(wc -l <$M) nonfile=$(awk -F'\t' '$4=="-"' $M|wc -l)"

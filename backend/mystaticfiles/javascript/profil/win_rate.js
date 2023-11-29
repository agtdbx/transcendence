/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   win_rate.js                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:24:57 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/24 17:22:22 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

function win_rate_calcul(win_rate) {
	document.getElementById("progg_bar_win_rate").style.width = "" +  (win_rate * 100) +  "%"; 
	let win_rate_indicator = document.getElementById("win_rate_indicator");
	win_rate_indicator.textContent = "" + win_rate * 100;
}
console.log("Win Rate Calcul");
win_rate_calcul(0.30);